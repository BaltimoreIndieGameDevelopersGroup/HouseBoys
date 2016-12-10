using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class CountDown : MonoBehaviour
{
    float timeLeft = 120.0f;
    public bool stop = true;

    private float minutes;
    private float seconds;
    public Text text;

    public void startTimer(float from)
    {
        stop = false;
        timeLeft = from;
        Update();
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

        GUI.Label(new Rect(10, 10, 250, 100), text.text);

        if (stop == true)
        {
            SceneManager.LoadScene("gameOver");
        }
    }
}
