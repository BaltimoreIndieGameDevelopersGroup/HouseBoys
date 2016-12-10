using System;
using UnityEngine;
using UnityEngine.Events;
using System.Collections;

namespace HouseBoys
{
    public class Destructible : MonoBehaviour
    {

        [Tooltip("Current health.")]
        public int health = 100;

        public UnityEvent onDestroy = new UnityEvent();

        [Tooltip("Instantiate this prefab when destroyed.")]
        public GameObject destroyedParticlePrefab;

        [Header("Health Bar")]

        public Canvas healthCanvas;
        public UnityEngine.UI.Slider healthSlider;
        public float healthBarVisibleDuration = 1;

        private PlayerController m_playerController;
       
        [Serializable]
        public class SpriteByHealth
        {
            public SpriteRenderer sprite;
            public int minHealth;
            public int maxHealth;
        }

        public SpriteByHealth[] spritesByHealth;

        void Start()
        {
            m_playerController = FindObjectOfType<PlayerController>();
            healthCanvas.gameObject.SetActive(false);
            healthSlider.maxValue = health;
            UpdateSprite();
        }

        void UpdateSprite()
        {
            healthSlider.value = health;
            foreach (var spriteByHealth in spritesByHealth)
            {
                spriteByHealth.sprite.gameObject.SetActive(spriteByHealth.minHealth <= health && health <= spriteByHealth.maxHealth);
            }
        }

        public void TakeDamage()
        {
            health -= 10;
            UpdateSprite();
            if (health <= 0)
            {
                DestroyMe();
            }
            else
            {
                ShowHealthBar();
            }
        }

        public void ShowHealthBar()
        {
            StopAllCoroutines();
            StartCoroutine(ShowHealthBarCoroutine());
        }

        private IEnumerator ShowHealthBarCoroutine()
        {
            healthCanvas.gameObject.SetActive(true);
            yield return new WaitForSeconds(healthBarVisibleDuration);
            healthCanvas.gameObject.SetActive(false);
        }

        public void DestroyMe()
        {
            onDestroy.Invoke();
            if (destroyedParticlePrefab != null) Instantiate(destroyedParticlePrefab, transform.position, transform.rotation);
            Destroy(gameObject);
        }

    }
}