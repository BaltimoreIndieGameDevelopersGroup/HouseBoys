using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HouseBoys
{
    public class Tool : MonoBehaviour
    {

        public void PickUp()
        {
            Debug.Log("PICK UP " + name, this);
            var playerController = FindObjectOfType<PlayerController>();
            Destroy(gameObject);
        }

    }
}