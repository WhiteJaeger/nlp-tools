context('NGram Metrics', () => {

    beforeEach(function () {
        cy.fixture('NGramMetrics').as('testData');
        cy.visit('/n-gram-metrics');
    })

    it('should check initial state', () => {
        cy.get('.head-content').should('contain', 'Sentence Level Translation Evaluation')
        cy.get('.head-content').should('contain', 'a given translation with N-gram based')
    })

    it('should write sentence in the form, submit form, check for the tagged words', function () {
        const {hypothesis, reference, metric, score, metricDisplayText} = this.testData.idealCase;

        cy.get('#input-text-hypothesis').type(hypothesis);
        cy.get('#input-text-reference').type(reference);
        cy.get('#metric-select').select(metric);
        cy.get('#metric-select option:selected').should('have.text', metricDisplayText);
        cy.get('#submit-button').click();

        cy.get('#result-container').should('be.visible');
        cy.get('#reference-text').should('contain.text', reference);
        cy.get('#hypothesis-text').should('contain.text', hypothesis);
        cy.get('#score').should('contain.text', score);
    })
})
