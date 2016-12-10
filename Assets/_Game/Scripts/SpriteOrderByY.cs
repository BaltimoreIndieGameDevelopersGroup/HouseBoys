using UnityEngine;

namespace HouseBoys
{

    public class SpriteOrderByY : MonoBehaviour
    {

        public bool isStationary;

        private SpriteRenderer m_spriteRenderer;

        private void Awake()
        {
            m_spriteRenderer = GetComponent<SpriteRenderer>();
            if (m_spriteRenderer == null)
            {
                Debug.LogError("No SpriteRenderer on " + name, this);
                enabled = false;
            }
        }

        void Start()
        {
            SetSpriteOrder();
            if (isStationary) Destroy(this);
        }

        void Update()
        {
            SetSpriteOrder();
        }

        void SetSpriteOrder()
        {
            m_spriteRenderer.sortingOrder = -Mathf.FloorToInt(transform.position.y * 100);
        }
    }
}
