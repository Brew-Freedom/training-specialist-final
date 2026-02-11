const { predictSentiment, addWord } = require('../script');

test('predict sentiment correctly', () => {
  positiveWords = ['good'];
  negativeWords = ['bad'];
  document.getElementById('userInput').value = 'I feel good';
  expect(predictSentiment()).toBe('Positive');
});

test('addWord adds new word', () => {
  positiveWords = ['good'];
  addWordTest('awesome', 'positive');
  expect(positiveWords.includes('awesome')).toBe(true);
});
