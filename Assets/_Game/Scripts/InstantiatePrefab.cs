using UnityEngine;

namespace HouseBoys
{

    public class InstantiatePrefab : MonoBehaviour
    {

        public void InstantiateHere(GameObject prefab)
        {
            var instance = Instantiate(prefab, transform.position, transform.rotation);
        }
 
    }
}