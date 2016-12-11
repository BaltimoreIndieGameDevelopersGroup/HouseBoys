using UnityEngine;
using UnityEngine.Events;
using System;

namespace HouseBoys
{

    public delegate void OnInteractableDestroyed(Interactable interactable);

    public class Interactable : MonoBehaviour
    {

        public const int InteractionLayer = 8;

        public event OnInteractableDestroyed interactableDestroyed = delegate{};

        public string playerAnimationTrigger;

        public UnityEvent onInteract = new UnityEvent();

        private void OnDestroy()
        {
            interactableDestroyed(this);
        }

        public void Interact(PlayerController playerController)
        {
            onInteract.Invoke();
            if (!string.IsNullOrEmpty(playerAnimationTrigger))
            {
                playerController.GetComponent<Animator>().SetTrigger(playerAnimationTrigger);
            }
        }
    }
}