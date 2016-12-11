using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace HouseBoys
{
    public class PlayerEffects : MonoBehaviour {

        public void PlayAnimation(string state)
        {
            StartCoroutine(PlayAnimAfterOneFrame(state));
        }

        private IEnumerator PlayAnimAfterOneFrame(string state)
        {
            yield return null;
            FindObjectOfType<PlayerController>().GetComponent<Animator>().Play(state);
        }

        public void PlayAudio(AudioClip audio)
        {
            var audioSource = GetComponent<AudioSource>();
            if (audioSource == null) audioSource = gameObject.AddComponent<AudioSource>();
            audioSource.PlayOneShot(audio);
        }

        public void StunPlayer(float seconds)
        {
            FindObjectOfType<PlayerController>().Stun(seconds);
        }
    }
}