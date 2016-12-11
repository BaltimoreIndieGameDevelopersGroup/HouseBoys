using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HouseBoys
{
    public class StartMenu : MonoBehaviour
    {

        // Use this for initialization
        void Start()
        {

        }

        public void Play()
        {
            UnityEngine.SceneManagement.SceneManager.LoadScene("Prototype");
        }
    }
}