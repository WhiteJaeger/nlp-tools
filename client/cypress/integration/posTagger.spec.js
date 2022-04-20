context('Part-of-speech Tagger', () => {
  beforeEach(() => {
    cy.visit('/pos-tagger')
  })

  it('should check initial state', () => {
    cy.get('.head-content').should('contain', 'Part-of-speech Tagger')
    cy.get('.head-content').should('contain', 'It was trained on the following NLTK corpora')
  })

  it('should write sentence in the form, submit form, check for the tagged words', () => {
    cy.fixture('POSTagger').then((fixture) => {
      cy.get('#input-text').type(fixture.ideal.text);
    });
    cy.get('#submit-button').click();
    cy.get('#result-container').should('be.visible');
    cy.get('#result-table').should('be.visible');
  })
})
