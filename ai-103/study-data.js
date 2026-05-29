// AI-103 Question Bank - Normalized Format
// Loads from questions.json
window.AI103_QUESTIONS = null;

(async function loadQuestions() {
  try {
    const resp = await fetch('./questions.json');
    const data = await resp.json();
    window.AI103_QUESTIONS = data;
    window.dispatchEvent(new CustomEvent('questionsLoaded', { detail: data }));
  } catch (e) {
    console.error('Failed to load questions.json:', e);
  }
})();
