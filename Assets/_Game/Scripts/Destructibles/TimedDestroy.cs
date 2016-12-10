using UnityEngine;
using UnityEngine.Events;
using System.Collections;

namespace HouseBoys
{

    public class TimedDestroy : MonoBehaviour
    {

        [Tooltip("Destroy the GameObject after this many seconds.")]
        public float duration = 1;

        [Tooltip("Run these events when destroying the GameObject.")]
        public UnityEvent onDestroy = new UnityEvent();

        IEnumerator Start()
        {
            yield return new WaitForSeconds(duration);
            onDestroy.Invoke();
            Destroy(gameObject);
        }
    }
}