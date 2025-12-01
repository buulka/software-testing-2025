describe('Successful Login', () => {
    it('Авторизация с корректными данными', () => {
    cy.visit('/login');
    cy.get('input[name="login"]').type('test_user');
    cy.get('input[name="password"]').type('test_password');
    cy.contains('Войти').click();

    cy.url().should('include', '/main');
    cy.contains('Добро пожаловать').should('be.visible');
    });
});
