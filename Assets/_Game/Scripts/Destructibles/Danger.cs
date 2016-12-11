using UnityEngine;
using UnityEngine.Events;

namespace HouseBoys
{

    public enum DangerCategory
    {
        None,
        Electrical,
        Water
    }

    public class Danger : MonoBehaviour
    {

        public DangerCategory dangerCategory;

        public UnityEvent onSuffer = new UnityEvent();

        public void Check()
        {
            var playerController = FindObjectOfType<PlayerController>();
            if (playerController != null && playerController.IsVulnerableTo(dangerCategory))
            {
                onSuffer.Invoke();
            }
        }

    }
}