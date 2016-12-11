using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

namespace HouseBoys
{
    public class StartEvent : MonoBehaviour
    {

        public UnityEvent onStart = new UnityEvent();

        void Start()
        {
            onStart.Invoke();
        }
    }
}