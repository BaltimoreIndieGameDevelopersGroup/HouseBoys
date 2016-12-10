using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StandinFloor : MonoBehaviour {

    public GameObject evenPrefab;
    public GameObject oddPrefab;

	void Start () {
        for (int i = -50; i <= 50; i++)
        {
            for (int j = -31; j <= 31; j++)
            {
                var prefab = ((i + j) % 2 == 0) ? evenPrefab : oddPrefab;
                var go = Instantiate(prefab, new Vector3(0.16f * i, 0.16f * j, 0), Quaternion.identity);
                go.transform.SetParent(transform);
            }
        }
	}
	
}