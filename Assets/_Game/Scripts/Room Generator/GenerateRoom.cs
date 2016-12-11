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

        public TextAsset[] jsonFiles;

        public bool randomLevels;

        [Header("Borders")]
        public GameObject horizontalBorder;
        public GameObject verticalBorder;

        [Header("Walls")]
        public GameObject horizontalWall;
        public GameObject verticalWall;
        public GameObject electricHorizontalWall;
        public GameObject plumbingWall;

        [Header("Floors")]
        public GameObject carpetFloor;
        public GameObject woodFloor;
        public GameObject tileFloor;

        [Header("Objects")]
        public GameObject bed;
        public GameObject toilet;
        public GameObject sofa;
        public GameObject stove;

        [Header("Tools")]
        public GameObject hammer;
        public GameObject rubberHammer;
        public GameObject plumbingWrench;

        public RoomDef roomDef;

        private const int TilesWide = 60;
        public const int TilesHigh = 40;

        void Start()
        {
            var jsonFile = randomLevels ? jsonFiles[UnityEngine.Random.Range(0, jsonFiles.Length)] : jsonFiles[0];

            roomDef = JsonUtility.FromJson<RoomDef>(jsonFile.text);

            // Floor:
            for (int x = 0; x < TilesWide; x++)
            {
                for (int y = 0; y < TilesHigh; y++)
                {
                    var tileCode = roomDef.tiles[x + y * TilesWide];
                    if (tileCode == "S" || tileCode == "W" || tileCode == "C") InstantiateTile(tileCode, x, y);
                }
            }

            //// Border:
            //for (int x = 0; x < TilesWide; x++)
            //{
            //    if (x % 4 == 0)
            //    {
            //        int y = -1;
            //        var go = Instantiate(horizontalBorder, new Vector3(0.16f * (x - TilesWide / 2), 0.16f * (y - TilesHigh / 2), 0), Quaternion.identity);
            //        go.transform.SetParent(transform);
            //        y = TilesHigh - 1;
            //        go = Instantiate(horizontalBorder, new Vector3(0.16f * (x - TilesWide / 2), 0.16f * (y - TilesHigh / 2), 0), Quaternion.identity);
            //        go.transform.SetParent(transform);
            //    }
            //}
            //for (int y = 0; y < TilesHigh; y ++)
            //{
            //    if (y % 3 == 0)
            //    {
            //        int x = 0;
            //        var go = Instantiate(verticalWall, new Vector3(0.16f * (x - TilesWide / 2), 0.16f * (y - TilesHigh / 2), 0), Quaternion.identity);
            //        go.transform.SetParent(transform);
            //        x = TilesWide - 2;
            //        go = Instantiate(verticalWall, new Vector3(0.16f + 0.16f * (x - TilesWide / 2), 0.16f * (y - TilesHigh / 2), 0), Quaternion.identity);
            //        go.transform.SetParent(transform);
            //    }
            //}


            // Vertical walls:
            for (var x = 0; x < TilesWide; x++)
            {
                var y = 0;
                while (y < TilesHigh)
                {
                    var tileCode = roomDef.tiles[x + y * TilesWide];
                    if (tileCode == "asdasdsa" || tileCode == "V")
                    {
                        InstantiateTile(tileCode, x + 1, y);
                        y += 3;
                    }
                    y++;
                }
            }

            // Horizontal walls:
            for (var y = 0; y < TilesHigh; y++)
            {
                var x = 0;
                while (x < TilesWide)
                {
                    var tileCode = roomDef.tiles[x + y * TilesWide];
                    if (tileCode == "H" || tileCode == "E")
                    {
                        InstantiateTile(tileCode, x, y, true);
                        x += 3;
                    }
                    x++;
                }
            }

            //// Tools:
            InstantiateTool("1");
            InstantiateTool("2");
            InstantiateTool("3");
            
            // Objects:
            //InstantiateObject(bed, UnityEngine.Random.Range(2, TilesWide - 1), UnityEngine.Random.Range(2, TilesHigh - 1));

        }

        private GameObject GetTilePrefab(string tileCode, bool doingHoriz)
        {
            switch (tileCode)
            {
                case "H":
                    var number = UnityEngine.Random.Range(0, 100);
                    return (number < 10) ? plumbingWall : (number < 20) ? electricHorizontalWall : horizontalWall;
                case "V":
                    return verticalWall;
                case "X":
                    return doingHoriz ? horizontalWall : verticalWall;
                case "E":
                    return doingHoriz ? electricHorizontalWall : verticalWall ;
                case "S":
                    return tileFloor;
                case "W":
                    return woodFloor;
                case "C":
                default:
                    return carpetFloor;
                case "1":
                    return hammer;
                case "2":
                    return rubberHammer;
                case "3":
                    return plumbingWrench;
                case "B":
                    return bed;
                case "T":
                    return toilet;
                case "R":
                    return stove;
                case "O":
                    return sofa;
            }

        }
        private void InstantiateTile(string tileCode, int x, int y, bool doingHoriz = false)
        {
            if (tileCode == "B" || tileCode == "T" || tileCode == "R" || tileCode == "O")
            {
                var prefab1 = (tileCode == "T") ? tileFloor : carpetFloor; ;
                var go1 = Instantiate(prefab1, new Vector3(0.16f * (x - TilesWide / 2), 0.16f * (y - TilesHigh / 2) + 0.16f, 0), Quaternion.identity);
                go1.transform.SetParent(transform);

            }
            var prefab = GetTilePrefab(tileCode, doingHoriz);
            float sx = (-((TilesWide / 2) * 0.16f)) + x * 0.16f;
            float sy = (-((TilesHigh / 2) * 0.16f)) + y * 0.16f;
            var go = Instantiate(prefab, new Vector3(sx, sy, 0), Quaternion.identity);
            go.transform.SetParent(transform);
        }

        private void InstantiateTool(string toolCode)
        {
            int safeguard = 0;
            do
            {
                var x = UnityEngine.Random.Range(2, TilesWide - 1);
                var y = UnityEngine.Random.Range(2, TilesHigh - 1);
                var tileCode = roomDef.tiles[x + y * TilesWide];
                if (tileCode == "C" || tileCode == "W" || tileCode == "S")
                {
                    InstantiateTile(toolCode, x, y);
                    return;
                }
                safeguard++;
            }
            while (safeguard < 99);
            InstantiateTile(toolCode, UnityEngine.Random.Range(2, TilesWide - 1), UnityEngine.Random.Range(2, TilesHigh - 1));
        }
    }
}