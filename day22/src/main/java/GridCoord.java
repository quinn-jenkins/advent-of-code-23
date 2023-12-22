public record GridCoord(int x, int y, int z)
{
    @Override
    public boolean equals(Object o)
    {
        if (this == o)
        {return true;}
        if (o == null || getClass() != o.getClass())
        {return false;}

        GridCoord gridCoord = (GridCoord) o;

        if (x != gridCoord.x)
        {return false;}
        if (y != gridCoord.y)
        {return false;}
        return z == gridCoord.z;
    }

    @Override
    public int hashCode()
    {
        int result = x;
        result = 31 * result + y;
        result = 31 * result + z;
        return result;
    }

    @Override
    public String toString()
    {
        return "GridCoord{" +
                "x=" + x +
                ", y=" + y +
                ", z=" + z +
                '}';
    }
}
