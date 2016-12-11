using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HouseBoys
{
    public class LoadLevelControl : MonoBehaviour
    {

        public void LoadLevel(string levelName)
        {
            UnityEngine.SceneManagement.SceneManager.LoadScene(levelName);
        }
    }
}