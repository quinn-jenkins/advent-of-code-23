import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Brick
{
    private final String name;
    private final GridCoord start;
    private final GridCoord end;

    private final List<GridCoord> brickSpan = new ArrayList<>();

    public Brick(String name, GridCoord start, GridCoord end)
    {
        this.name = name;
        this.start = start;
        this.end = end;

        for (int x = start.x(); x <= end.x(); x++)
        {
            for (int y = start.y(); y <= end.y(); y++)
            {
                for (int z = start.z(); z <= end.z(); z++)
                {
                    brickSpan.add(new GridCoord(x, y, z));
                }
            }
        }
    }

    public String getName()
    {
        return this.name;
    }

    public List<GridCoord> getBrickSpan()
    {
        return Collections.unmodifiableList(brickSpan);
    }

    public boolean supportsOtherBrick(Brick other)
    {
        if (getName().equals(other.getName()))
        {
            return false;
        }
        for (GridCoord supportedPos : other.getBrickSpan())
        {
            for (GridCoord brickPos : getBrickSpan())
            {
                if (supportedPos.z() - brickPos.z() == 1 && supportedPos.x() == brickPos.x() && supportedPos.y() == brickPos.y())
                {
                    return true;
                }
            }
        }
        return false;
    }

    public Brick shiftBrickDown(int newZ)
    {
        GridCoord newStart = new GridCoord(start.x(), start.y(), newZ);
        GridCoord newEnd = new GridCoord(end.x(), end.y(), newZ);
        return new Brick(name, newStart, newEnd);
    }

    @Override
    public String toString()
    {
        return "Brick{" +
                "name='" + name + '\'' +
                ", start=" + start +
                ", end=" + end +
                ", brickSpan=" + brickSpan +
                '}';
    }

    @Override
    public boolean equals(Object o)
    {
        if (this == o)
        {return true;}
        if (o == null || getClass() != o.getClass())
        {return false;}

        Brick brick = (Brick) o;

        if (!name.equals(brick.name))
        {return false;}
        if (!start.equals(brick.start))
        {return false;}
        return end.equals(brick.end);
    }

    @Override
    public int hashCode()
    {
        int result = name.hashCode();
        result = 31 * result + start.hashCode();
        result = 31 * result + end.hashCode();
        return result;
    }
}
