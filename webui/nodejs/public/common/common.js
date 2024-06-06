export function displaySelectedTeamName(teamName) {
    const selectedTeamNameElement = document.getElementById('selectedTeamNameDisplay');
    selectedTeamNameElement.textContent = `${teamName}`;
}