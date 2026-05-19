using System;

public enum PokeType
{
    Normal, Fire, Water, Grass, Electric, Ice, Fighting, Poison, Ground,
    Flying, Psychic, Bug, Rock, Ghost, Dragon, Dark, Steel, Fairy, Null
};

class Type
{
    private static readonly string[] TypeNames=new string[19]
    {
        "ノーマル　","ほのお　　","みず　　　","くさ　　　","でんき　　","こおり　　","かくとう　","どく　　　","じめん　　","ひこう　　","エスパー　","むし　　　","いわ　　　","ゴースト　","ドラゴン　","あく　　　","はがね　　","フェアリー","　　　　　"
    };

    private static readonly float[,] MatchupTable = new float[19, 19]
    {
        // 防御側: Nor, Fir, Wat, Gra, Ele, Ice, Fig, Poi, Gro, Fly, Psy, Bug, Roc, Gho, Dra, Dar, Ste, Fai, Nul
        /* Normal   */ { 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 0.5f, 0.0f, 1.0f, 1.0f, 0.5f, 1.0f, 1.0f },
        /* Fire     */ { 1.0f, 0.5f, 0.5f, 2.0f, 1.0f, 2.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 2.0f, 0.5f, 1.0f, 0.5f, 1.0f, 2.0f, 1.0f, 1.0f },
        /* Water    */ { 1.0f, 2.0f, 0.5f, 0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 2.0f, 1.0f, 1.0f, 1.0f, 2.0f, 1.0f, 0.5f, 1.0f, 1.0f, 1.0f, 1.0f },
        /* Grass    */ { 1.0f, 0.5f, 2.0f, 0.5f, 1.0f, 1.0f, 1.0f, 0.5f, 2.0f, 0.5f, 1.0f, 0.5f, 2.0f, 1.0f, 0.5f, 1.0f, 0.5f, 1.0f, 1.0f },
        /* Electric */ { 1.0f, 1.0f, 2.0f, 0.5f, 0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 2.0f, 1.0f, 1.0f, 1.0f, 1.0f, 0.5f, 1.0f, 1.0f, 1.0f, 1.0f },
        /* Ice      */ { 1.0f, 0.5f, 0.5f, 2.0f, 1.0f, 0.5f, 1.0f, 1.0f, 2.0f, 2.0f, 1.0f, 1.0f, 1.0f, 1.0f, 2.0f, 1.0f, 0.5f, 1.0f, 1.0f },
        /* Fighting */ { 2.0f, 1.0f, 1.0f, 1.0f, 1.0f, 2.0f, 1.0f, 0.5f, 1.0f, 0.5f, 0.5f, 0.5f, 2.0f, 0.0f, 1.0f, 2.0f, 2.0f, 0.5f, 1.0f },
        /* Poison   */ { 1.0f, 1.0f, 1.0f, 2.0f, 1.0f, 1.0f, 1.0f, 0.5f, 0.5f, 1.0f, 1.0f, 1.0f, 0.5f, 0.5f, 1.0f, 1.0f, 0.0f, 2.0f, 1.0f },
        /* Ground   */ { 1.0f, 2.0f, 1.0f, 0.5f, 2.0f, 1.0f, 1.0f, 2.0f, 1.0f, 0.0f, 1.0f, 0.5f, 2.0f, 1.0f, 1.0f, 1.0f, 2.0f, 1.0f, 1.0f },
        /* Flying   */ { 1.0f, 1.0f, 1.0f, 2.0f, 0.5f, 1.0f, 2.0f, 1.0f, 1.0f, 1.0f, 1.0f, 2.0f, 0.5f, 1.0f, 1.0f, 1.0f, 0.5f, 1.0f, 1.0f },
        /* Psychic  */ { 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 2.0f, 2.0f, 1.0f, 1.0f, 0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 0.0f, 0.5f, 1.0f, 1.0f },
        /* Bug      */ { 1.0f, 0.5f, 1.0f, 2.0f, 1.0f, 1.0f, 0.5f, 0.5f, 1.0f, 0.5f, 2.0f, 1.0f, 1.0f, 0.5f, 1.0f, 2.0f, 0.5f, 0.5f, 1.0f },
        /* Rock     */ { 1.0f, 2.0f, 1.0f, 1.0f, 1.0f, 2.0f, 0.5f, 1.0f, 0.5f, 2.0f, 1.0f, 2.0f, 1.0f, 1.0f, 1.0f, 1.0f, 0.5f, 1.0f, 1.0f },
        /* Ghost    */ { 0.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 2.0f, 1.0f, 1.0f, 2.0f, 1.0f, 0.5f, 1.0f, 1.0f, 1.0f },
        /* Dragon   */ { 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 2.0f, 1.0f, 0.5f, 0.0f, 1.0f },
        /* Dark     */ { 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 0.5f, 1.0f, 1.0f, 1.0f, 2.0f, 1.0f, 1.0f, 2.0f, 1.0f, 0.5f, 1.0f, 0.5f, 1.0f },
        /* Steel    */ { 1.0f, 0.5f, 0.5f, 1.0f, 0.5f, 2.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 2.0f, 1.0f, 1.0f, 1.0f, 0.5f, 2.0f, 1.0f },
        /* Fairy    */ { 1.0f, 0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 2.0f, 0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 2.0f, 2.0f, 0.5f, 1.0f, 1.0f },
        /* Null     */ { 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f }
    };

    public static float TypeMatchup(PokeType attacker, PokeType defender1, PokeType defender2)
    {
        // defender2 が Null の場合は計算をスキップして最適化
        if (defender2 == PokeType.Null)
        {
            return MatchupTable[(int)attacker, (int)defender1];
        }
        return MatchupTable[(int)attacker, (int)defender1] * MatchupTable[(int)attacker, (int)defender2];
    }

    private static string TypeName(PokeType type)
    {
        return TypeNames[(int)type];
    }

    public static void AllMatchups(PokeType attacker)
    {
        Console.WriteLine($"【{TypeName(attacker)}のタイプ相性一覧】");
        
        for (int i = 0; i < 18; i++)
        {
            // 1. 単タイプの出力
            PokeType def1 = (PokeType)i;
            float singleEffect = TypeMatchup(attacker, def1, PokeType.Null);
            Console.WriteLine($"{TypeName(def1)}: {singleEffect}倍");

            // 2. 複合タイプの出力
            for (int j = i + 1; j < 18; j++)
            {
                PokeType def2 = (PokeType)j;
                float dualEffect = TypeMatchup(attacker, def1, def2);
                
                // 倍率が1.0倍の場合は表示を省略するなどの制御も可能ですが、
                // 今回は全て出力するようにしています
                Console.WriteLine($"{TypeName(def1)}・{TypeName(def2)}: {dualEffect}倍");
            }
        }
    }
}

class Program
{
    public static void Main()
    {
        Type.AllMatchups(PokeType.Fire);
    }
}