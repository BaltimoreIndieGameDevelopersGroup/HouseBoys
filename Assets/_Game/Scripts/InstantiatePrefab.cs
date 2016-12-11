using UnityEngine;

namespace HouseBoys
{

    public class InstantiatePrefab : MonoBehaviour
    {

        public void InstantiateHere(GameObject prefab)
        {
            Instantiate(prefab, transform.position, transform.rotation);
        }
 
    }
}