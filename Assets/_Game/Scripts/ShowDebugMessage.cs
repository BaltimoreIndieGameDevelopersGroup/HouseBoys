using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ShowDebugMessage : MonoBehaviour {

    public void ShowMessage(string message)
    {
        Debug.Log(message, this);
	}
}
