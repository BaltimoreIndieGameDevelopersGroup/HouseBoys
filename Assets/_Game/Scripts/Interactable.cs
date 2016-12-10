using UnityEngine;
using UnityEngine.Events;
using System;

namespace HouseBoys
{

    public delegate void OnInteractableDestroyed(Interactable interactable);

    public class Interactable : MonoBehaviour
    {

        public event OnInteractableDestroyed interactableDestroyed = delegate{};

        public string playerAnimationTrigger;

        public GameObjectUnityEvent onInteract = new GameObjectUnityEvent();

        private void OnDestroy()
        {
            interactableDestroyed(this);
        }

        public void Interact(PlayerController playerController)
        {
            onInteract.Invoke(playerController.gameObject);
            if (!string.IsNullOrEmpty(playerAnimationTrigger))
            {
                playerController.GetComponent<Animator>().SetTrigger(playerAnimationTrigger);
            }
        }
    }
}