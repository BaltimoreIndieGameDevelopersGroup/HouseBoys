using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

namespace HouseBoys
{

    [Serializable]
    public class RoomDef
    {
        public int difficulty;
        public string[] tiles;
        public int number;
        public int timer;
    }
    public class GenerateRoom : MonoBehaviour
    {

        public TextAsset jsonFile;

        [Header("Borders")]
        public GameObject horizontalBorder;
        public GameObject verticalBorder;

        [Header("Walls")]
        public GameObject horizontalWall;
        public GameObject verticalWall;
        public GameObject floor;

        [Header("Objects")]
        public GameObject bed;

        [Header("Tools")]
        public GameObject hammer;
        public GameObject rubberHammer;
        public GameObject plumbingWrench;

        public RoomDef roomDef;

        private const int TilesWide = 60;
        public const int TilesHigh = 40;

        void Start()
        {
            roomDef = JsonUtility.FromJson<RoomDef>(jsonFile.text);

            // Floor:
            for (int i = -50; i <= 50; i++)
            {
                for (int j = -31; j <= 31; j++)
                {
                    var prefab = floor;
                    var go = Instantiate(prefab, new Vector3(0.16f * i, 0.16f * j, 0), Quaternion.identity);
                    go.transform.SetParent(transform);
                }
            }
            
            // Border:
            for (int x = 0; x < TilesWide; x++)
            {
                if (x % 4 == 0)
                {
                    int y = -1;
                    var go = Instantiate(horizontalBorder, new Vector3(0.16f * (x - TilesWide / 2), 0.16f * (y - TilesHigh / 2), 0), Quaternion.identity);
                    go.transform.SetParent(transform);
                    y = TilesHigh - 1;
                    go = Instantiate(horizontalBorder, new Vector3(0.16f * (x - TilesWide / 2), 0.16f * (y - TilesHigh / 2), 0), Quaternion.identity);
                    go.transform.SetParent(transform);
                }
            }
            for (int y = 0; y < TilesHigh; y ++)
            {
                if (y % 3 == 0)
                {
                    int x = 0;
                    var go = Instantiate(verticalWall, new Vector3(0.16f * (x - TilesWide / 2), 0.16f * (y - TilesHigh / 2), 0), Quaternion.identity);
                    go.transform.SetParent(transform);
                    x = TilesWide - 2;
                    go = Instantiate(verticalWall, new Vector3(0.16f + 0.16f * (x - TilesWide / 2), 0.16f * (y - TilesHigh / 2), 0), Quaternion.identity);
                    go.transform.SetParent(transform);
                }
            }


            // Vertical walls:
            for (var x = 0; x < TilesWide; x++)
            {
                var y = TilesHigh - 1;
                while (y >= 0)
                {
                    var tileCode = roomDef.tiles[x + y * TilesWide];
                    if (tileCode == "C" || tileCode == "V")
                    {
                        var go = Instantiate(verticalWall, new Vector3(0.16f + 0.16f * (x - TilesWide / 2), 0.16f * (y - TilesHigh / 2) - 0.48f, 0), Quaternion.identity);
                        go.transform.SetParent(transform);
                        y -= 3;
                    }
                    y--;
                }
            }

            // Horizontal walls:
            for (var y = 0; y < TilesHigh; y++)
            {
                var x = 0;
                while (x < TilesWide)
                {
                    var tileCode = roomDef.tiles[x + y * TilesWide];
                    if (tileCode == "H")
                    {
                        var go = Instantiate(horizontalWall, new Vector3(0.16f * (x - TilesWide / 2), 0.16f * (y - TilesHigh / 2), 0), Quaternion.identity);
                        go.transform.SetParent(transform);
                        x += 3;
                    }
                    x++;
                }
            }

            // Tools:
            InstantiateObject(hammer, UnityEngine.Random.Range(2, TilesWide - 1), UnityEngine.Random.Range(2, TilesHigh - 1));
            InstantiateObject(rubberHammer, UnityEngine.Random.Range(2, TilesWide - 1), UnityEngine.Random.Range(2, TilesHigh - 1));
            InstantiateObject(plumbingWrench, UnityEngine.Random.Range(2, TilesWide - 1), UnityEngine.Random.Range(2, TilesHigh - 1));

            // Objects:
            InstantiateObject(bed, UnityEngine.Random.Range(2, TilesWide - 1), UnityEngine.Random.Range(2, TilesHigh - 1));

        }

        private void InstantiateObject(GameObject prefab, int x, int y)
        {
            var go = Instantiate(prefab, new Vector3(0.16f * (x - TilesWide / 2), 0.16f * (y - TilesHigh / 2) + 0.16f, 0), Quaternion.identity);
            go.transform.SetParent(transform);

        }
    }
}