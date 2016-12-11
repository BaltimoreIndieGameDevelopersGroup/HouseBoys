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

        public int totalWalls = 0;

        public UnityEngine.UI.Text wallsLeftText;

        public UnityEngine.UI.Slider wallSlider;

        private void Awake()
        {
            m_instance = this;
        }

        public void AddDestructible(DestructibleCategory category)
        {
            if (category == DestructibleCategory.Wall)
            {
                wallsLeft++;
                totalWalls = Mathf.Max(totalWalls, wallsLeft);
                wallSlider.maxValue = totalWalls;
                UpdateScore();
            }
        }

        public void RemoveDestructible(DestructibleCategory category)
        {
            switch (category)
            {
                case DestructibleCategory.Wall:
                    wallsLeft--;
                    UpdateScore();
                    if (wallsLeft <= 0) Win();
                    break;
                case DestructibleCategory.Penalty:
                    break;
                case DestructibleCategory.Bonus:
                    break;
            }
        }

        public void UpdateScore()
        {
            wallsLeftText.text = wallsLeft.ToString();
            wallSlider.value = totalWalls - wallsLeft;
        }

        public void Win()
        {
            Debug.Log("WIN!");
            UnityEngine.SceneManagement.SceneManager.LoadScene("win", UnityEngine.SceneManagement.LoadSceneMode.Additive);
        }
    }

}