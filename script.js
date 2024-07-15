document.addEventListener('DOMContentLoaded', () => {
    const modelCards = document.querySelectorAll('.model-card');

    modelCards.forEach(card => {
        const hoverImage = card.getAttribute('data-hover');
        const originalImage = card.style.backgroundImage;
        card.addEventListener('mouseover', () => {
            card.style.backgroundImage = `url('${hoverImage}')`;
        });
        card.addEventListener('mouseout', () => {
            card.style.backgroundImage = originalImage;
        });
    });

    const form = document.getElementById('votingForm');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const selectedDress = form.elements['dress'].value;
        if (selectedDress) {
            // Increment vote count in local storage
            const votes = JSON.parse(localStorage.getItem('votes')) || {};
            votes[selectedDress] = (votes[selectedDress] || 0) + 1;
            localStorage.setItem('votes', JSON.stringify(votes));

            const discountCode = `CODE-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;
            document.getElementById('discountCode').textContent = discountCode;
            document.getElementById('voteResult').style.display = 'block';
        } else {
            alert('Please select a dress to vote.');
        }
    });

    document.getElementById('copyCodeBtn').addEventListener('click', () => {
        const discountCode = document.getElementById('discountCode').textContent;
        navigator.clipboard.writeText(discountCode).then(() => {
            alert('Discount code copied to clipboard!');
        });
    });

    // Function to get the voting results
    window.getVotingResults = () => {
        const votes = JSON.parse(localStorage.getItem('votes')) || {};
        const sortedVotes = Object.entries(votes).sort((a, b) => b[1] - a[1]);
        return sortedVotes;
    };
});
