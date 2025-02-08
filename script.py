import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1️⃣ Configurer ChromeOptions pour utiliser le port de débogage et le profil existant
options = Options()
options.debugger_address = (
    "localhost:9222"  # Connexion à l'instance existante de Chrome
)

# 2️⃣ Lancer Selenium avec la configuration d'options (pas de nouvelle fenêtre)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# 3️⃣ Vérifier que la connexion a bien été établie avec le navigateur déjà ouvert
print("✅ Connexion à Chrome existant réussie!")

# 4️⃣ Accéder à l'onglet Instagram
target_url = "https://www.instagram.com/your_activity/interactions/likes/"

found = False
while not found:
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if target_url in driver.current_url:
            print("✅ Onglet Instagram trouvé!")
            found = True
            break
    time.sleep(1)

# Boucle infinie pour répéter les étapes 5 à 8 avec 1 minute d'intervalle
try:
    while True:
        # 5️⃣ Attendre que le bouton "Sélectionner" soit visible et cliquer dessus
        try:
            select_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//*[@id='mount_0_0_TE']/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/article/div/div[2]/div/div/div[1]/div/div/div/div/div[2]/div[2]",
                    )
                )
            )
            select_button.click()
            print("✅ Bouton 'Sélectionner' cliqué.")
            time.sleep(2)
        except Exception as e:
            print("⚠ Erreur : Impossible de cliquer sur 'Sélectionner'.", e)

        # 6️⃣ Localiser la div contenant les images et sélectionner les 5 divs enfants directs
        try:
            # Trouver la div contenant les 5 images
            div_images = driver.find_element(
                By.XPATH,
                "//*[@id='mount_0_0_TE']/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/article/div/div[2]/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[1]/div",
            )

            # Trouver toutes les div descendantes directes dans cette div
            liked_posts = div_images.find_elements(
                By.XPATH, "./div"
            )  # Sélectionner toutes les div directes enfants

            # Limiter à 5 images
            for i in range(min(5, len(liked_posts))):  # Sélectionner jusqu'à 5 images
                liked_posts[i].click()
                time.sleep(0.5)
            print("✅ 5 images sélectionnées.")
        except Exception as e:
            print("⚠ Erreur lors de la sélection des images.", e)

        # 7️⃣ Cliquer sur "Je n’aime plus" (nouveau XPath)
        try:
            unlike_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//*[@id='mount_0_0_TE']/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/article/div/div[2]/div/div/div[1]/div/div/div/div/div[4]/div/div/div[2]/div/div/div[2]/div/div/div/div/div[1]/div/span",
                    )
                )
            )
            unlike_button.click()
            print("✅ Premier clic sur 'Je n’aime plus'.")
        except Exception as e:
            print("⚠ Erreur lors du 'Je n’aime plus'.", e)

        # 8️⃣ Cliquer sur le dernier bouton (nouveau XPath)
        try:
            last_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/button[1]",
                    )
                )
            )
            last_button.click()
            print("✅ Dernier bouton cliqué.")
        except Exception as e:
            print("⚠ Erreur lors du clic sur le dernier bouton.", e)

        # 9️⃣ Attendre 1 minute avant de répéter
        print("⏳ Attente de 1 minute avant la prochaine répétition...")
        time.sleep(60)  # Attente de 60 secondes (1 minute)

except KeyboardInterrupt:
    print("🔴 Le script a été arrêté manuellement.")
