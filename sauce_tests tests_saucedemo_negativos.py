import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"

def test_ct01_visualizacao_senha(page: Page):
    """CT-01: Tentativa de visualizar os caracteres da senha digitada (Negativo)"""
    page.goto(BASE_URL)
    password_input = page.locator("#password")
    password_input.fill("secret_sauce")
    expect(password_input).to_have_attribute("type", "password")

def test_ct02_login_usuario_bloqueado(page: Page):
    """CT-02: Tentativa de login com usuário bloqueado - locked_out_user (Negativo)"""
    page.goto(BASE_URL)
    page.locator("#user-name").fill("locked_out_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    error_msg = page.locator("[data-test='error']")
    expect(error_msg).to_be_visible()
    expect(error_msg).to_contain_text("Sorry, this user has been locked out")

def test_ct07_problem_user_imagens(page: Page):
    """CT-07: Verificação de imagens inconsistentes no problem_user (Negativo/Bug)"""
    page.goto(BASE_URL)
    page.locator("#user-name").fill("problem_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    img = page.locator(".inventory_item:first-child img")
    src = img.get_attribute("src")
    assert src is not None

def test_ct10_problem_user_erro_about(page: Page):
    """CT-10: Erro/redirecionamento ao clicar em About com problem_user (Negativo)"""
    page.goto(BASE_URL)
    page.locator("#user-name").fill("problem_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    page.locator("#react-burger-menu-btn").click()
    about_link = page.locator("#about_sidebar_link")
    expect(about_link).to_be_visible()
    about_link.click()
    page.wait_for_timeout(2000)
    assert "saucelabs.com" not in page.url or page.url == "https://www.saucedemo.com/"

def test_ct16_performance_glitch_carrinho(page: Page):
    """CT-16: Adição automática com performance_glitch_user (Negativo)"""
    page.goto(BASE_URL)
    page.locator("#user-name").fill("performance_glitch_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    page.wait_for_timeout(3000)
    assert page.url == "https://www.saucedemo.com/inventory.html"

def test_ct10_happy_path_positivo(page: Page):
    """CT-10 (Positivo): Fluxo completo de compra bem-sucedido"""
    page.goto(BASE_URL)
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    page.locator("#add-to-cart-sauce-labs-backpack").click()
    page.locator(".shopping_cart_link").click()
    page.locator("#checkout").click()
    page.locator("#first-name").fill("Ruan")
    page.locator("#last-name").fill("Oliveira")
    page.locator("#postal-code").fill("44570000")
    page.locator("#continue").click()
    page.locator("#finish").click()

    success_header = page.locator(".complete-header")
    expect(success_header).to_contain_text("Thank you for your order!")
