using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

namespace HouseBoys
{
    public class TimedEvent : MonoBehaviour
    {

        public float timeToWait = 1;

        public UnityEvent onTime = new UnityEvent();

        IEnumerator Start()
        {
            yield return new WaitForSeconds(timeToWait);
            onTime.Invoke();
        }

    }
}