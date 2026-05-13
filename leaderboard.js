// ================= BACK BUTTON ================= //

document.getElementById('backBtn')
.addEventListener('click', () => {

    window.location.href = 'index.html';

});


// ================= CURRENT USER ================= //

const currentUser =
    sessionStorage.getItem('userName');


// ================= LOAD LEADERBOARD ================= //

async function loadLeaderboard() {

    try {

        const response =
            await fetch(
                'http://127.0.0.1:8000/leaderboard'
            );

        const data =
            await response.json();

        // ================= TOP 3 ================= //

        if (data.length > 0) {

            document.getElementById('rank1Name')
            .innerText = data[0].username;

            document.getElementById('rank1Score')
            .innerText =
                `${data[0].score} pts`;

        }

        if (data.length > 1) {

            document.getElementById('rank2Name')
            .innerText = data[1].username;

            document.getElementById('rank2Score')
            .innerText =
                `${data[1].score} pts`;

        }

        if (data.length > 2) {

            document.getElementById('rank3Name')
            .innerText = data[2].username;

            document.getElementById('rank3Score')
            .innerText =
                `${data[2].score} pts`;

        }

        // ================= TABLE ================= //

        const tbody =
            document.getElementById('leaderboardBody');

        tbody.innerHTML = "";

        data.forEach((user, index) => {

            const row =
                document.createElement('tr');

            // ================= CURRENT USER HIGHLIGHT ================= //

            if (user.username === currentUser) {

                row.classList.add('current-user');

            }

            row.innerHTML = `
                <td>

                    #${index + 1}

                </td>

                <td>

                    ${user.username}

                </td>

                <td>

                    ${user.score} pts

                </td>
            `;

            tbody.appendChild(row);

        });

    } catch (err) {

        console.log(
            "Leaderboard load failed"
        );

    }

}


// ================= INITIAL LOAD ================= //

loadLeaderboard();