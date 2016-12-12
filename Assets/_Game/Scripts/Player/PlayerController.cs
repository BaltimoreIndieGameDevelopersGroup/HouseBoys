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

        private float m_stunnedTimeLeft = 0;

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
            m_stunnedTimeLeft = Mathf.Max(0, m_stunnedTimeLeft - Time.deltaTime);
            if (IsStunned()) return;

            if (UnityEngine.EventSystems.EventSystem.current.IsPointerOverGameObject()) return;

            if (Input.GetMouseButton(0))
            {
                m_destinationPosition = Camera.main.ScreenToWorldPoint(Input.mousePosition);
                destinationMarker.transform.position = m_destinationPosition;
            }
            if (Input.GetMouseButtonUp(0))
            {
                var ray = Camera.main.ScreenPointToRay(Input.mousePosition);
                var hits = Physics2D.RaycastAll(ray.origin, ray.direction, Mathf.Infinity, 1 << Interactable.InteractionLayer);
                foreach (var hit in hits)
                {
                    var hitInteractable = hit.collider.GetComponent<Interactable>();
                    if (hitInteractable != null)
                    {
                        if (!m_nearbyInteractables.Contains(hitInteractable))
                        {
                            m_destinationInteractable = hitInteractable;
                        }
                        else
                        {
                            hitInteractable.Interact(this);
                        }
                        return;
                    }
                }
            }
        }

        private bool runTrue; // hacky quick fix.

        private void FixedUpdate()
        {
            if (IsStunned())
            {
                m_rigidbody2D.velocity = Vector2.zero;
                return;
            }

            // Move the character:
            var direction = m_destinationPosition - new Vector2(transform.position.x, transform.position.y);
            var move = new Vector2(Mathf.Abs(direction.x) > 0.1f ? Mathf.Sign(m_destinationPosition.x - transform.position.x) * maxHorizontalSpeed : 0, 
                Mathf.Abs(direction.y) > 0.1f ? Mathf.Sign(m_destinationPosition.y - transform.position.y) * maxVerticalSpeed : 0);
            m_rigidbody2D.velocity = move.magnitude > 0.5f ? move : Vector2.zero;

            var newRunTrue = move.magnitude > 0.5f;
            if (newRunTrue != runTrue)
            {
                runTrue = newRunTrue;
                // Update the animator:
                m_animator.SetBool(RunParameter, newRunTrue);//  move.magnitude > 0.5f);
            }

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
            if (newInteractable == m_destinationInteractable)
            {
                m_destinationInteractable.Interact(this);
                m_destinationInteractable = null;
            }
        }

        private void OnTriggerExit2D(Collider2D other)
        {
            var oldInteractable = other.GetComponent<Interactable>();
            if (oldInteractable != null) m_nearbyInteractables.Remove(oldInteractable);
        }

        private void OnInteractableDestroyed(Interactable interactable)
        {
            m_nearbyInteractables.Remove(interactable);
        }

        public void UseTool(Tool tool)
        {
            currentTool = tool;
        }

        public int GetToolDamage(Destructible destructible)
        {
            return (currentTool == null) ? 10 : currentTool.damage;
        }

        public bool IsVulnerableTo(DangerCategory dangerCategory)
        {
            if (dangerCategory == DangerCategory.None) return false;
            if (currentTool == null) return true;
            return currentTool.protectsAgainst != dangerCategory;
        }

        public void Stun(float duration)
        {
            m_animator.SetBool(RunParameter, false);
            m_stunnedTimeLeft = duration;
        }

        public bool IsStunned()
        {
            return m_stunnedTimeLeft > 0.01;
        }

    }
}