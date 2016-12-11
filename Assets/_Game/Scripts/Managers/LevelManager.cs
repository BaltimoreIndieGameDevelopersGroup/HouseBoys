using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HouseBoys
{

    public class LevelManager : MonoBehaviour
    {

        public static LevelManager instance { get { return m_instance; } }

        private static LevelManager m_instance = null;

        public int wallsLeft = 0;

        public UnityEngine.UI.Text wallsLeftText;

        private void Awake()
        {
            m_instance = this;
        }

        public void AddDestructible(DestructibleCategory category)
        {
            if (category == DestructibleCategory.Wall)
            {
                wallsLeft++;
                wallsLeftText.text = wallsLeft.ToString();
            }
        }

        public void RemoveDestructible(DestructibleCategory category)
        {
            switch (category)
            {
                case DestructibleCategory.Wall:
                    wallsLeft--;
                    wallsLeftText.text = wallsLeft.ToString();
                    if (wallsLeft <= 0) Win();
                    break;
                case DestructibleCategory.Penalty:
                    break;
                case DestructibleCategory.Bonus:
                    break;
            }
        }

        public void Win()
        {
            Debug.Log("WIN!");
            UnityEngine.SceneManagement.SceneManager.LoadScene("win", UnityEngine.SceneManagement.LoadSceneMode.Additive);
        }
    }

}