// utils.js
function calculateAverageForTerm(termPerformances) {
    if (termPerformances.length === 0) {
        return 0;
    }

    const sum = termPerformances.reduce((acc, val) => acc + val, 0);
    return sum / termPerformances.length;
}