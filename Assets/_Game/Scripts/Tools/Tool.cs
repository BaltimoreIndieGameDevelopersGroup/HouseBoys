using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HouseBoys
{

    public class Tool : MonoBehaviour
    {

        public int damage;

        public DangerCategory protectsAgainst = DangerCategory.None;

        public void PickUp()
        {
            var playerController = FindObjectOfType<PlayerController>();
            if (playerController.currentTool != null) playerController.currentTool.Drop();
            playerController.UseTool(this);
            transform.SetParent(playerController.transform);
            foreach (Transform child in transform)
            {
                child.gameObject.SetActive(false);
            }
        }

        public void Drop()
        {
            var playerController = FindObjectOfType<PlayerController>();
            playerController.currentTool = null;
            transform.SetParent(null);
            transform.position = playerController.transform.position;
            foreach (Transform child in transform)
            {
                child.gameObject.SetActive(true);
            }
        }

    }
}