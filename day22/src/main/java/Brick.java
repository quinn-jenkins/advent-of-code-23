import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Brick
{
    private final int brickId;
    private final GridCoord start;
    private final GridCoord end;

    private final List<GridCoord> brickSpan = new ArrayList<>();

    public Brick(int brickId, GridCoord start, GridCoord end)
    {
        this.brickId = brickId;
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

    public int getBrickId()
    {
        return brickId;
    }

    public List<GridCoord> getBrickSpan()
    {
        return Collections.unmodifiableList(brickSpan);
    }

    public int getMaxZ()
    {
        int highestZ = 0;
        for (GridCoord gridCoord : getBrickSpan())
        {
            highestZ = Math.max(highestZ, gridCoord.z());
        }
        return highestZ;
    }

    public int getDeltaZ()
    {
        return end.z() - start.z();
    }

    public boolean supportsOtherBrick(Brick other)
    {
        if (getBrickId() == other.getBrickId())
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
        int deltaZ = end.z() - start.z();
        GridCoord newStart = new GridCoord(start.x(), start.y(), newZ);
        GridCoord newEnd = new GridCoord(end.x(), end.y(), newZ + deltaZ);
        return new Brick(brickId, newStart, newEnd);
    }

    @Override
    public String toString()
    {
        return "Brick{" +
                "name='" + brickId + '\'' +
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

        if (brickId != brick.brickId)
        {return false;}
        if (!start.equals(brick.start))
        {return false;}
        return end.equals(brick.end);
    }

    @Override
    public int hashCode()
    {
        int result = brickId;
        result = 31 * result + start.hashCode();
        result = 31 * result + end.hashCode();
        return result;
    }
}
