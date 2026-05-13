// ================= NAVIGATION CONTROLS ================= //

const navHome =
    document.getElementById('navHome');

const navChallenges =
    document.getElementById('navChallenges');

const navLeaderboard =
    document.getElementById('navLeaderboard');

const homeView =
    document.getElementById('home-view');

const challengesView =
    document.getElementById('challenges-view');


// ================= HOME ================= //

navHome.onclick = () => {

    challengesView.classList.add('hidden');

    homeView.classList.remove('hidden');

    navHome.classList.add('active');

    navChallenges.classList.remove('active');

};


// ================= CHALLENGES ================= //

navChallenges.onclick = () => {

    homeView.classList.add('hidden');

    challengesView.classList.remove('hidden');

    navHome.classList.remove('active');

    navChallenges.classList.add('active');

};


// ================= LEADERBOARD ================= //

navLeaderboard.onclick = () => {

    window.location.href =
        'leaderboard.html';

};


// ================= AUTH ================= //

if (sessionStorage.getItem('isLoggedIn') !== 'true') {

    window.location.href = 'auth.html';

}

const currentUserName =
    sessionStorage.getItem('userName') || "User";

const currentUserEmail =
    sessionStorage.getItem('userEmail') || "No Email";


// ================= USER UI ================= //

document.getElementById('welcome-text').innerText =
    `Welcome back, ${currentUserName} 👋`;

document.getElementById('profile-name').innerText =
    currentUserName;

document.getElementById('profile-email').innerText =
    currentUserEmail;

document.getElementById('navInitial').innerText =
    currentUserName.charAt(0).toUpperCase();

document.getElementById('cardInitial').innerText =
    currentUserName.charAt(0).toUpperCase();


// ================= LOGOUT ================= //

document.querySelector('.logout-btn')
.addEventListener('click', () => {

    sessionStorage.clear();

    window.location.href = 'auth.html';

});


// ================= MODALS ================= //

const aiModal =
    document.getElementById('aiModal');

const aboutModal =
    document.getElementById('aboutModal');

document.getElementById('askAiBtn').onclick = () => {

    aiModal.style.display = 'flex';

};

document.getElementById('closeAi').onclick = () => {

    aiModal.style.display = 'none';

};

document.getElementById('openAboutBtn').onclick = () => {

    aboutModal.style.display = 'flex';

};

document.getElementById('closeAbout').onclick = () => {

    aboutModal.style.display = 'none';

};

window.onclick = (e) => {

    if (e.target == aiModal)
        aiModal.style.display = 'none';

    if (e.target == aboutModal)
        aboutModal.style.display = 'none';

};


// ================= PROFILE DROPDOWN ================= //

const profileToggle =
    document.getElementById('profileToggle');

const profileCard =
    document.getElementById('profileCard');

profileToggle.onclick = (e) => {

    profileCard.classList.toggle('show');

    e.stopPropagation();

};

document.onclick = () => {

    profileCard.classList.remove('show');

};

profileCard.onclick = (e) => {

    e.stopPropagation();

};


// ================= PROFILE PHOTO ================= //

document.getElementById('photoInp').onchange = function () {

    const file = this.files[0];

    if (file) {

        const reader = new FileReader();

        reader.onload = (e) => {

            const imgHtml =
                `<img src="${e.target.result}" class="avatar-img">`;

            document.getElementById('profileToggle')
                .innerHTML = imgHtml;

            document.getElementById('cardAvatar')
                .innerHTML = imgHtml;

        };

        reader.readAsDataURL(file);

    }

};


// ================= PERFORMANCE CHART ================= //

const ctx =
    document.getElementById("chart");

if (ctx) {

    new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: [
                "Solved",
                "Incorrect",
                "Pending"
            ],

            datasets: [{

                data: [60, 20, 20],

                backgroundColor: [
                    "#6366f1",
                    "#ef4444",
                    "#10b981"
                ]

            }]

        },

        options: {

            plugins: {

                legend: {

                    display: false

                }

            }

        }

    });

}


// ================= AI RESULT BOX ================= //

const aiResultBox =
    document.createElement('div');

aiResultBox.id = 'aiResult';

aiResultBox.style.cssText = `
    margin-top: 8px;
    padding: 10px;
    background: #f1f5f9;
    border-radius: 8px;
    font-size: 14px;
    line-height: 1.5;
    color: #1e293b;
    white-space: pre-wrap;
    max-height: 420px;
    overflow-y: auto;
    display: none;
`;

document.getElementById('aiPrompt')
.insertAdjacentElement('afterend', aiResultBox);


// ================= BUTTON REFERENCES ================= //

const answerBtn =
    document.getElementById('submitAi');


// ================= CREATE QUIZ BUTTON ================= //

const quizBtn =
    document.createElement('button');

quizBtn.id = "takeQuizBtn";

quizBtn.innerText = "Take Quiz";

quizBtn.style.cssText = `
    margin-left:10px;
    padding:10px 16px;
    border:none;
    border-radius:8px;
    background:#10b981;
    color:white;
    cursor:pointer;
    font-weight:600;
`;


// ================= ADD BUTTON NEXT TO GET ANSWER ================= //

answerBtn.parentNode.insertBefore(
    quizBtn,
    answerBtn.nextSibling
);


// ================= GLOBAL QUIZ STORAGE ================= //

let latestQuizData = null;

let latestPrompt = "";


// ================= GET ANSWER ================= //

answerBtn.addEventListener('click', async () => {

    const prompt =
        document.getElementById('aiPrompt')
        .value.trim();

    if (!prompt) {

        alert('Please type a question first!');

        return;

    }

    latestPrompt = prompt;

    answerBtn.innerText = "Thinking...";

    answerBtn.disabled = true;

    aiResultBox.style.display = 'none';

    try {

        const response =
            await fetch(
                `http://127.0.0.1:8000/ask-ai?question=${encodeURIComponent(prompt)}`
            );

        const data =
            await response.json();

        latestQuizData = data.quiz;

        aiResultBox.innerHTML = `
            <div style="
                line-height:1.6;
            ">
                ${data.explanation}
            </div>
        `;

        aiResultBox.style.display = 'block';

    } catch (err) {

        aiResultBox.innerHTML =
            "⚠️ Could not reach backend.";

        aiResultBox.style.display = 'block';

    } finally {

        answerBtn.innerText =
            "Get Answer";

        answerBtn.disabled = false;

    }

});


// ================= TAKE QUIZ ================= //

quizBtn.addEventListener('click', async () => {

    if (!latestQuizData) {

        alert(
            "First click 'Get Answer' to generate quiz."
        );

        return;

    }

    let html = `
        <h3 style="
            margin-bottom:10px;
            color:#6366f1;
        ">
            Quiz Time 🚀
        </h3>
    `;

    latestQuizData.forEach((q, index) => {

        html += `
            <div style="
                margin-bottom:8px;
                padding:8px;
                background:white;
                border-radius:6px;
                border:1px solid #e2e8f0;
            ">

                <p style="
                    font-weight:600;
                    margin-bottom:4px;
                    font-size:14px;
                ">
                    Q${index + 1}: ${q.question}
                </p>
        `;

        q.options.forEach(option => {

            html += `
                <label style="
                    display:flex;
                    align-items:center;
                    gap:5px;
                    margin-bottom:2px;
                    cursor:pointer;
                ">

                    <input
                        type="radio"
                        name="quiz_${index}"
                        value="${option}"
                        style="
                            width:14px;
                            height:14px;
                            margin:0;
                        "
                    >

                    <span style="
                        font-size:13px;
                    ">
                        ${option}
                    </span>

                </label>
            `;

        });

        html += `</div>`;

    });

    html += `
        <button id="submitQuizBtn"
            style="
                margin-top:8px;
                padding:8px 14px;
                border:none;
                border-radius:8px;
                background:#6366f1;
                color:white;
                cursor:pointer;
                font-weight:600;
            ">
            Submit Quiz
        </button>

        <div id="quizScore"
            style="
                margin-top:10px;
            ">
        </div>
    `;

    aiResultBox.innerHTML = html;

    aiResultBox.style.display = 'block';

    // ================= QUIZ SUBMIT ================= //

    document.getElementById('submitQuizBtn')
    .addEventListener('click', async () => {

        let score = 0;

        let resultHTML = "";

        latestQuizData.forEach((q, index) => {

            const selected =
                document.querySelector(
                    `input[name="quiz_${index}"]:checked`
                );

            const userAnswer =
                selected
                    ? selected.value
                    : "Not Answered";

            const isCorrect =
                userAnswer === q.answer;

            // ================= SCORE ================= //

            if (isCorrect) {

                score += 10;

            }

            // ================= RESULT CARD ================= //

            resultHTML += `
                <div style="
                    margin-top:10px;
                    padding:10px;
                    border-radius:8px;
                    background:${isCorrect ? '#ecfdf5' : '#fef2f2'};
                    border:1px solid ${isCorrect ? '#10b981' : '#ef4444'};
                ">

                    <p style="
                        font-weight:600;
                        margin-bottom:6px;
                        color:${isCorrect ? '#10b981' : '#ef4444'};
                    ">
                        Q${index + 1}
                        ${isCorrect ? '✅ Correct' : '❌ Wrong'}
                    </p>

                    <p>
                        <strong>Your Answer:</strong>
                        ${userAnswer}
                    </p>

                    <p>
                        <strong>Correct Answer:</strong>
                        ${q.answer}
                    </p>

                </div>
            `;

        });

        // ================= FINAL SCORE ================= //

        resultHTML += `
            <div style="
                margin-top:15px;
                padding:12px;
                background:#eef2ff;
                border-radius:10px;
                font-weight:bold;
                text-align:center;
                font-size:16px;
            ">
                🎉 Final Score: ${score}
            </div>
        `;

        document.getElementById('quizScore')
        .innerHTML = resultHTML;

        // ================= SAVE SCORE ================= //

        await fetch(
    `http://127.0.0.1:8000/submit-score?username=${currentUserName}&topic=${encodeURIComponent(latestPrompt)}&score=${score}`,
    {
        method: 'POST'
    }
);

// REFRESH USER STATS

loadUserStats();

    });

});

// ================= USER STATS ================= //

async function loadUserStats() {

    try {

        const response =
            await fetch(
                'http://127.0.0.1:8000/leaderboard'
            );

        const data =
            await response.json();

        let currentRank = 0;

        let currentPoints = 0;

        data.forEach((user, index) => {

            if (
                user.username === currentUserName
            ) {

                currentRank =
                    index + 1;

                currentPoints =
                    user.score;

            }

        });

        // UPDATE POINTS

        const pointsElement =
            document.getElementById('userPoints');

        if (pointsElement) {

            pointsElement.innerText =
                currentPoints;

        }

        // UPDATE RANK

        const rankElement =
            document.getElementById('userRank');

        if (rankElement) {

            rankElement.innerText =
                `#${currentRank}`;

        }

    } catch (err) {

        console.log(
            "Could not load stats"
        );

    }

}


// ================= INITIAL LOAD ================= //

loadUserStats();

// ================= SIDEBAR TOGGLE ================= //

const menuBtn =
    document.getElementById('menuBtn');

const chatSidebar =
    document.getElementById('chatSidebar');


// ================= OPEN/CLOSE ================= //

menuBtn.addEventListener('click', (e) => {

    e.stopPropagation();

    chatSidebar.classList.toggle('open');

});


// ================= CLOSE ON OUTSIDE CLICK ================= //

document.addEventListener('click', (e) => {

    if (
        !chatSidebar.contains(e.target) &&
        !menuBtn.contains(e.target)
    ) {

        chatSidebar.classList.remove('open');

    }

});