using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace HouseBoys
{

    public class PlayerController : MonoBehaviour
    {

        public string horizontalAxis = "Horizontal";
        public string verticalAxis = "Vertical";

        [Tooltip("The fastest the player can travel left and right.")]
        public float maxHorizontalSpeed = 8f;

        [Tooltip("The fastest the player can travel up and down.")]
        public float maxVerticalSpeed = 5f;

        [Tooltip("Tracks which direction the player is facing.")]
        public bool facingLeft = false;

        public Tool currentTool;

        public GameObject destinationMarker;

        private Rigidbody2D m_rigidbody2D;
        private Animator m_animator;
        private SpriteOrderByY m_spriteOrderByY;

        private const string RunParameter = "Run";
        private const string AttackParameter = "Attack";

        [SerializeField]
        private Vector2 m_destinationPosition;

        [SerializeField]
        private Interactable m_destinationInteractable;

        [SerializeField]
        private List<Interactable> m_nearbyInteractables = new List<Interactable>();

        private void Awake()
        {
            m_rigidbody2D = GetComponent<Rigidbody2D>();
            m_animator = GetComponent<Animator>();
            m_spriteOrderByY = GetComponent<SpriteOrderByY>();
            if (m_rigidbody2D == null) Debug.LogError("No Rigidbody2D found on " + name, this);
            if (m_animator == null) Debug.LogError("No Animator found on " + name, this);
            if (m_spriteOrderByY == null) m_spriteOrderByY = gameObject.AddComponent<SpriteOrderByY>();
        }

        private void Start()
        {
            m_destinationPosition = transform.position;
        }

        private void Update()
        {
            if (Input.GetMouseButton(0))
            {
                m_destinationPosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
                destinationMarker.transform.position = m_destinationPosition;
            }
            if (Input.GetMouseButtonUp(0))
            {
                var ray = Camera.main.ScreenPointToRay(Input.mousePosition);
                var hit = Physics2D.Raycast(ray.origin, ray.direction, Mathf.Infinity, 1 << 8);
                m_destinationInteractable = (hit.collider != null) ? hit.collider.GetComponent<Interactable>() : null;
                InteractWithNearbyInteractables();
            }
        }

        private void FixedUpdate()
        {
            // Move the character:
            var direction = m_destinationPosition - new Vector2(transform.position.x, transform.position.y);
            var move = new Vector2(Mathf.Abs(direction.x) > 0.1f ? Mathf.Sign(m_destinationPosition.x - transform.position.x) * maxHorizontalSpeed : 0, 
                Mathf.Abs(direction.y) > 0.1f ? Mathf.Sign(m_destinationPosition.y - transform.position.y) * maxVerticalSpeed : 0);
            m_rigidbody2D.velocity = move.magnitude > 0.5f ? move : Vector2.zero;

            // Update the animator:
            m_animator.SetBool(RunParameter, move.magnitude > 0.5f);

            // Flip the character if necessary:
            var needToFlip = ((move.x < 0 && !facingLeft) || (move.x > 0 && facingLeft));
            if (needToFlip)
            {
                facingLeft = !facingLeft;
                Vector3 scale = transform.localScale;
                scale.x *= -1;
                transform.localScale = scale;
            }
        }

        private void OnTriggerEnter2D(Collider2D other)
        {
            var newInteractable = other.GetComponent<Interactable>();
            if (newInteractable == null) return;
            m_nearbyInteractables.Add(newInteractable);
            newInteractable.interactableDestroyed += OnInteractableDestroyed;
            if (newInteractable == m_destinationInteractable) newInteractable.Interact(this);
        }

        private void OnTriggerExit2D(Collider2D other)
        {
            var oldInteractable = other.GetComponent<Interactable>();
            if (oldInteractable == null) return;
            m_nearbyInteractables.Remove(oldInteractable);
        }

        private void OnInteractableDestroyed(Interactable interactable)
        {
            m_nearbyInteractables.Remove(interactable);
        }

        private void InteractWithNearbyInteractables()
        {
            for (int i = 0; i < m_nearbyInteractables.Count; i++)
            {
                m_nearbyInteractables[i].Interact(this);
            }
        }

    }
}