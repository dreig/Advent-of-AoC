{- stack script --resolver lts-18.18 -}
import System.Environment
import Data.List (foldl')

data Instruction a = Noop | Forward a | Up a | Down a

solveP1 contents = let (dist, depth) = foldl' addInstructionP1 (0,0)
                                      . parseContents
                                      $ contents
                    in dist * depth

solveP2 contents = let (_, dist, depth) = foldl' addInstructionP2 (0,0,0)
                                          . parseContents
                                          $ contents
                    in dist * depth

addInstructionP2 (aim, x, y) (Forward a)  = (aim, x+a, y+aim*a)
addInstructionP2 (aim, x, y) (Up a)       = (aim-a, x,y)
addInstructionP2 (aim, x, y) (Down a)    = (aim+a, x,y)
addInstructionP2 (aim, x, y) Noop         = (aim, x, y)

addInstructionP1 (x,y) (Forward a) = (x+a,y)
addInstructionP1 (x,y) (Up a)      = (x,y-a)
addInstructionP1 (x,y) (Down a)    = (x,y+a)
addInstructionP1 (x,y) Noop        = (x,y)

getInstruction line = case words line of
  ["forward", x] -> Forward (read x :: Integer)
  ["up",      x] -> Up (read x :: Integer)
  ["down",    x] -> Down (read x :: Integer)
  _              -> Noop

parseContents = map getInstruction . filter (not . null) . lines

main = do
  args <- getArgs
  contents <- readFile $ head args
  putStrLn $ "Part 1: " ++ show (solveP1 contents)
  putStrLn $ "Part 2: " ++ show (solveP2 contents)
