describe('Login Error Handling', () => {
    it('Отображение ошибки при неверных данных', () => {
    cy.visit('/login');
    cy.get('input[name="login"]').type('wrong_user');
    cy.get('input[name="password"]').type('wrong_pass');
    cy.contains('Войти').click();

    cy.contains('Неверный логин или пароль').should('be.visible');
    });
});
