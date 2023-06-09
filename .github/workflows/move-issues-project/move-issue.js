const { Octokit } = require("@octokit/rest");

const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

async function moveIssue() {
  const issue = await octokit.rest.issues.get({
    owner: "silvio",
    repo: "test_automation_github_issues"
  });

  const currentStatus = issue.state;

  const aprovado = "Aprovado";
  const validando = "Validando";
  const pronto = "Pronto";

  let nextStatus;

  if (currentStatus === aprovado) {
    nextStatus = validando;
  } else if (currentStatus === validando) {
    nextStatus = pronto;
  } else {
    return "Nenhuma issue a ser movida";
  }

  await octokit.rest.issues.update({
    owner: "silvio",
    repo: "test_automation_github_issues",
    issue_number: issue.number,
    state: nextStatus,
  });
}

moveIssue();