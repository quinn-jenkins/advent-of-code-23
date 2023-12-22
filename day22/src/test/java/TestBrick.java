import org.junit.jupiter.api.Test;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

public class TestBrick
{
    @Test
    public void test_brick_span()
    {
        Brick brick = new Brick("A", new GridCoord(0, 0, 1), new GridCoord(0, 0, 3));
        List<GridCoord> span = brick.getBrickSpan();
        assertThat(new GridCoord(0, 0, 1)).isIn(span);
        assertThat(new GridCoord(0, 0, 2)).isIn(span);
        assertThat(new GridCoord(0, 0, 3)).isIn(span);

        brick = new Brick("A", new GridCoord(1, 0, 0), new GridCoord(3, 0, 0));
        span = brick.getBrickSpan();
        assertThat(new GridCoord(1, 0, 0)).isIn(span);
        assertThat(new GridCoord(2, 0, 0)).isIn(span);
        assertThat(new GridCoord(3, 0, 0)).isIn(span);

        brick = new Brick("A", new GridCoord(0, 1, 0), new GridCoord(0, 3, 0));
        span = brick.getBrickSpan();
        assertThat(new GridCoord(0, 1, 0)).isIn(span);
        assertThat(new GridCoord(0, 2, 0)).isIn(span);
        assertThat(new GridCoord(0, 3, 0)).isIn(span);
    }

    @Test
    public void test_brick_is_supporting()
    {
        Brick supporting = new Brick("A", new GridCoord(0, 0, 0), new GridCoord(0, 0, 1));
        Brick supported = new Brick("A", new GridCoord(0, 0, 2), new GridCoord(0, 1, 2));
        assertThat(supporting.supportsOtherBrick(supported)).isTrue();

        supporting = new Brick("A", new GridCoord(0, 0, 0), new GridCoord(0, 2, 0));
        supported = new Brick("A", new GridCoord(0, 0, 1), new GridCoord(0, 1, 1));
        assertThat(supporting.supportsOtherBrick(supported)).isTrue();

        supporting = new Brick("A", new GridCoord(0, 0, 0), new GridCoord(2, 0, 0));
        supported = new Brick("A", new GridCoord(0, 0, 1), new GridCoord(1, 0, 1));
        assertThat(supporting.supportsOtherBrick(supported)).isTrue();

        // bricks don't line up
        supporting = new Brick("A", new GridCoord(0, 0, 0), new GridCoord(2, 0, 0));
        supported = new Brick("A", new GridCoord(0, 1, 1), new GridCoord(0, 2, 1));
        assertThat(supporting.supportsOtherBrick(supported)).isFalse();

        // supported brick is not directly above the supporting brick
        supporting = new Brick("A", new GridCoord(0, 0, 0), new GridCoord(2, 0, 0));
        supported = new Brick("A", new GridCoord(0, 1, 2), new GridCoord(0, 2, 2));
        assertThat(supporting.supportsOtherBrick(supported)).isFalse();
    }
}
