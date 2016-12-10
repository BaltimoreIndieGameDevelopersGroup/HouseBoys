using System.Collections;
using UnityEngine;

namespace HouseBoys
{
    public class ScreenShake : MonoBehaviour
    {

        public float shakeAmount = 0.2f;
        public float duration = 1;

        public void Shake()
        {
            StartCoroutine(ShakeCoroutine());
        }

        IEnumerator ShakeCoroutine()
        {
            var originalLocalPosition = Camera.main.transform.localPosition;
            var elapsed = 0f;
            while (elapsed < duration)
            {
                var pos = Random.insideUnitCircle * shakeAmount;
                Camera.main.transform.localPosition = new Vector3(pos.x, pos.y, Camera.main.transform.localPosition.z);
                elapsed += Time.deltaTime;
                yield return null;
            }
            Camera.main.transform.localPosition = originalLocalPosition;
            yield return null;
        }
    }
}
