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

        public GameObject horizontalWall;
        public GameObject verticalWall;
        public GameObject floor;

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

            // Vertical walls:
            for (var x = 0; x < TilesWide; x++)
            {
                var y = TilesHigh - 1;
                while (y >= 0)
                {
                    var tileCode = roomDef.tiles[x + y * TilesWide];
                    if (tileCode == "C" || tileCode == "V")
                    {
                        var go = Instantiate(verticalWall, new Vector3(0.16f * (x - TilesWide / 2), 0.16f * (y - TilesHigh / 2), 0), Quaternion.identity);
                        go.transform.SetParent(transform);
                        y -= 2;
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
                    if (tileCode == "C" || tileCode == "H")
                    {
                        var go = Instantiate(horizontalWall, new Vector3(0.16f * (x - TilesWide / 2), 0.16f * (y - TilesHigh / 2), 0), Quaternion.identity);
                        go.transform.SetParent(transform);
                        x += 2;
                    }
                    x++;
                }
            }

        }

    }
}