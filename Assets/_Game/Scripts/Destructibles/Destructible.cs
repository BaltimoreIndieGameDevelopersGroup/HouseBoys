using System;
using UnityEngine;
using UnityEngine.Events;
using System.Collections;

namespace HouseBoys
{

    public enum DestructibleCategory
    {
        Wall,
        Bonus,
        Penalty
    }

    public class Destructible : MonoBehaviour
    {

        public DestructibleCategory category = DestructibleCategory.Wall;


        [Tooltip("Current health.")]
        public int health = 100;

        public float invulnerableDuration = 0.5f;

        public UnityEvent onTakeDamage = new UnityEvent();
        public UnityEvent onDestroy = new UnityEvent();

        [Tooltip("Instantiate this prefab when destroyed.")]
        public GameObject destroyedParticlePrefab;

        [Header("Health Bar")]

        public Canvas healthCanvas;
        public UnityEngine.UI.Slider healthSlider;
        public float healthBarVisibleDuration = 1;

        private PlayerController m_playerController;
        private bool m_isInvulnerable;
       
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
            LevelManager.instance.AddDestructible(category);
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
            if (m_isInvulnerable)
            {
                ShowHealthBar();
                return;
            }
            health -= m_playerController.GetToolDamage(this);
            UpdateSprite();
            if (health <= 0)
            {
                DestroyMe();
            }
            else
            {
                ShowHealthBar();
                m_isInvulnerable = true;
                Invoke("BecomeVulnerable", invulnerableDuration);
            }
            onTakeDamage.Invoke();
        }

        private void BecomeVulnerable()
        {
            m_isInvulnerable = false;
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
            LevelManager.instance.RemoveDestructible(category);
        }

    }
}