using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

namespace HouseBoys
{
    public class TimerScript : MonoBehaviour
    {
        public float timeLeft = 120.0f;
        public float warningTime = 10f;
        public bool stop = true;

        private float minutes;
        private float seconds;
        public Text text;

        private void Start()
        {
            startTimer(timeLeft);
        }

        public void startTimer(float from)
        {
            stop = false;
            timeLeft = from;
        }

        void Update()
        {
            timeLeft -= Time.deltaTime;

            minutes = Mathf.Floor(timeLeft / 60);
            seconds = timeLeft % 60;
            if (seconds > 59) seconds = 59;
            if (minutes < 0)
            {
                stop = true;
                minutes = 0;
                seconds = 0;
            }

            text.text = string.Format("{0:0}:{1:00}", minutes, seconds);
            if (timeLeft < warningTime) text.text = "<color=red>" + text.text + "</color>";

            if (stop == true)
            {
                var levelManager = FindObjectOfType<LevelManager>();
                if (levelManager.AreWinConditionsTrue())
                {
                    levelManager.Win();
                }
                else
                {
                    SceneManager.LoadScene("gameOver", LoadSceneMode.Additive);
                }
                GetComponent<AudioSource>().Stop();
                Destroy(this);
                
            }
        }
    }
}