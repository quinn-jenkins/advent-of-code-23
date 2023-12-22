import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Set;
import java.util.concurrent.LinkedBlockingQueue;

public class day22
{
    private static final Logger logger = LoggerFactory.getLogger(day22.class);

    public static void main(String[] args)
    {
        new day22();
    }

    public day22()
    {
        try
        {
            List<String> allLines = Files.readAllLines(Paths.get("src/main/resources/input.txt"));
            partOne(allLines);
        } catch (Exception e)
        {
            logger.error("Caught exception", e);
        }
    }

    private void partOne(List<String> puzzle)
    {
        List<Brick> bricks = new ArrayList<>();
        Map<Integer, List<Brick>> bricksByLayer = new HashMap<>();
        int maxX = 0;
        int maxY = 0;
        int brickId = 0;
        for (String brickString : puzzle)
        {
            String[] parts = brickString.split("~");
            Integer[] startCoords = convertToInts(parts[0].split(","));
            Integer[] endCoords = convertToInts(parts[1].split(","));
            GridCoord start = new GridCoord(startCoords[0], startCoords[1], startCoords[2]);
            GridCoord end = new GridCoord(endCoords[0], endCoords[1], endCoords[2]);
            Brick brick = new Brick("" + brickId, start, end);
            bricks.add(brick);
            int zStart = start.z();
            int zEnd = end.z();
            for (int z = zStart; z <= zEnd; z++)
            {
                bricksByLayer.computeIfAbsent(z, k -> new ArrayList<>()).add(brick);
            }
            maxX = Math.max(start.x(), maxX);
            maxX = Math.max(end.x(), maxX);
            maxY = Math.max(start.y(), maxY);
            maxY = Math.max(end.y(), maxY);
            brickId++;
        }

        Map<Integer, List<Brick>> fallenBricks = completeFallingBricks(bricksByLayer, maxX, maxY);

        List<Brick> layerBelow = null;
        Map<String, List<String>> supportingBricks = new HashMap<>();
        for (Brick b : bricks)
        {
            supportingBricks.put(b.getName(), new ArrayList<>());
        }
        for (Map.Entry<Integer, List<Brick>> entry : fallenBricks.entrySet())
        {
            if (layerBelow == null)
            {
                layerBelow = entry.getValue();
                continue;
            }

            for (Brick possibleSuppportingBrick : layerBelow)
            {
                for (Brick brick : entry.getValue())
                {
                    if (possibleSuppportingBrick.supportsOtherBrick(brick))
                    {
                        supportingBricks.get(possibleSuppportingBrick.getName()).add(brick.getName());
                    }
                }
            }

            layerBelow = entry.getValue();
        }

        Map<String, List<String>> supportedByMap = invertMap(supportingBricks);
        Set<String> freeBricks = new HashSet<>();
        List<String> bricksSupportingOthers = new ArrayList<>();
        for (Map.Entry<String, List<String>> entry : supportingBricks.entrySet())
        {
            if (entry.getValue().isEmpty())
            {
                freeBricks.add(entry.getKey());
            }
            boolean allSupportedMoreThanOnce = true;
            for (String supportedBrick : entry.getValue())
            {
                if (supportedByMap.get(supportedBrick).size() <= 1)
                {
                    allSupportedMoreThanOnce = false;
                    break;
                }
            }
            if (allSupportedMoreThanOnce)
            {
                freeBricks.add(entry.getKey());
            } else
            {
                bricksSupportingOthers.add(entry.getKey());
            }
        }

        logger.info("Part One: {}", freeBricks.size());

        int sum = 0;
        for (String brick : bricksSupportingOthers)
        {
            sum += getChainReactionSize(brick, supportingBricks, supportedByMap);
        }

        logger.info("Part Two: {}", sum);

    }

    /**
     * Supporting Bricks: Key is supporting each of the bricks in the value list
     * Bricks Supported By: Key is supported by each of the bricks in the value list
     */
    private int getChainReactionSize(String brick, Map<String, List<String>> supportingBricks, Map<String, List<String>> bricksSupportedBy)
    {
        int numDisintegrated = 0;
        Set<String> disintegratedBricks = new HashSet<>();
        Queue<String> brickQueue = new LinkedBlockingQueue<>();
        brickQueue.add(brick);

        while (!brickQueue.isEmpty())
        {
            String currentBrick = brickQueue.poll();
            disintegratedBricks.add(currentBrick);
            for (String supportedBrick : supportingBricks.get(currentBrick))
            {
                List<String> bricksHoldingThisBrick = bricksSupportedBy.get(supportedBrick);
                bricksHoldingThisBrick.removeAll(disintegratedBricks);
                if (bricksHoldingThisBrick.isEmpty())
                {
                    numDisintegrated++;
                    brickQueue.add(supportedBrick);
                }
            }
        }
        logger.info("{} bricks fall when {} is disintegrated", numDisintegrated, brick);
        return numDisintegrated;
    }

    private Map<String, List<String>> invertMap(Map<String, List<String>> orig)
    {
        Map<String, List<String>> inverted = new HashMap<>();
        for (Map.Entry<String, List<String>> entry : orig.entrySet())
        {
            for (String s : entry.getValue())
            {
                inverted.computeIfAbsent(s, k -> new ArrayList<>()).add(entry.getKey());
            }
        }
        return inverted;
    }

    private Map<Integer, List<Brick>> completeFallingBricks(Map<Integer, List<Brick>> startingBricks, int widthX, int widthY)
    {
        Map<Integer, List<Brick>> fallenBricks = new HashMap<>();
        int[][] highestBrickAtXY = new int[widthX + 1][widthY + 1];
        for (Map.Entry<Integer, List<Brick>> entry : startingBricks.entrySet())
        {
            for (Brick b : entry.getValue())
            {
                int highestSupport = 0;
                for (GridCoord gridCoord : b.getBrickSpan())
                {
                    highestSupport = Math.max(highestBrickAtXY[gridCoord.x()][gridCoord.y()], highestSupport);
                }
                int brickSettledLayer = highestSupport + 1;
                Brick newBrick = b.shiftBrickDown(brickSettledLayer);
                fallenBricks.computeIfAbsent(brickSettledLayer, k -> new ArrayList<>()).add(newBrick);
                // we're supported, so see if we update the highest point anywhere
                for (GridCoord gridCoord : newBrick.getBrickSpan())
                {
                    int currentHighest = highestBrickAtXY[gridCoord.x()][gridCoord.y()];
                    if (gridCoord.z() > currentHighest)
                    {
                        highestBrickAtXY[gridCoord.x()][gridCoord.y()] = gridCoord.z();
                    }
                }
            }
        }

        return fallenBricks;
    }

    private Integer[] convertToInts(String[] numbers)
    {
        Integer[] ints = new Integer[numbers.length];
        for (int i = 0; i < numbers.length; i++)
        {
            int val = Integer.parseInt(numbers[i]);
            ints[i] = val;
        }
        return ints;
    }
}
