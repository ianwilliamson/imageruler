"""Regular shapes."""

from typing import Tuple
import numpy as np


def rounded_square(
    resolution: float,
    phys_size: Tuple[float, float],
    declared_mls: float,
    center: Tuple[float, float] = (0, 0),
    angle: float = 0,
) -> np.ndarray:
  """Return a Boolean array where all True elements form a square with rounded corners.

  Args:
      resolution: A float that represents the number of points per unit length.
      phys_size: A tuple with two elements that describe the physical size of
        the entire pattern.
      declared_mls: A float that represents the declared minimum length scale,
        which is equal to the diameter of round corners.
      center: A tuple with two elements that describe the coordinates of the
        center of the square.
      angle: A float that represents the angle of rotation in degree.

  Returns:
      An array with Boolean elements.
  """

  phys_size = np.array(phys_size)
  angle = np.radians(angle)

  n = np.round(phys_size * resolution).astype(
      int
  )  # number of pixels along each dimension
  grid_size = (
      n - 1
  ) / resolution  # size of the entire pattern formed by centers of pixels

  x_coord = np.linspace(-grid_size[0] / 2, grid_size[0] / 2, n[0])
  y_coord = np.linspace(-grid_size[1] / 2, grid_size[1] / 2, n[1])
  xv, yv = np.meshgrid(x_coord, y_coord, sparse=True, indexing='ij')

  side, diameter = 2 * declared_mls, declared_mls
  rect_vert = (
      abs(np.sin(angle) * (xv - center[0]) - np.cos(angle) * (yv - center[1]))
      <= (side - diameter) / 2
  ) & (
      abs(np.cos(angle) * (xv - center[0]) + np.sin(angle) * (yv - center[1]))
      <= side / 2
  )
  rect_hori = (
      abs(np.sin(angle) * (xv - center[0]) - np.cos(angle) * (yv - center[1]))
      <= side / 2
  ) & (
      abs(np.cos(angle) * (xv - center[0]) + np.sin(angle) * (yv - center[1]))
      <= (side - diameter) / 2
  )

  disc_centers = (
      np.array([
          [
              side - diameter,
              diameter - side,
              diameter - side,
              side - diameter,
          ],
          [
              side - diameter,
              side - diameter,
              diameter - side,
              diameter - side,
          ],
      ])
      / 2
  )
  disc_centers_x = (
      disc_centers[0, :] * np.cos(angle)
      - disc_centers[1, :] * np.sin(angle)
      + center[0]
  )
  disc_centers_y = (
      disc_centers[0, :] * np.sin(angle)
      + disc_centers[1, :] * np.cos(angle)
      + center[1]
  )
  disc_centers = np.vstack((disc_centers_x, disc_centers_y))

  disc0 = (xv - disc_centers[0, 0]) ** 2 + (
      yv - disc_centers[1, 0]
  ) ** 2 <= diameter**2 / 4
  disc1 = (xv - disc_centers[0, 1]) ** 2 + (
      yv - disc_centers[1, 1]
  ) ** 2 <= diameter**2 / 4
  disc2 = (xv - disc_centers[0, 2]) ** 2 + (
      yv - disc_centers[1, 2]
  ) ** 2 <= diameter**2 / 4
  disc3 = (xv - disc_centers[0, 3]) ** 2 + (
      yv - disc_centers[1, 3]
  ) ** 2 <= diameter**2 / 4

  return rect_vert | rect_hori | disc0 | disc1 | disc2 | disc3


def disc(
    resolution: float,
    phys_size: Tuple[float, float],
    diameter: float,
    center: Tuple[float, float] = (0, 0),
) -> np.ndarray:
  """Return a Boolean array where all True elements form a disc.

  Args:
      resolution: A float that represents the number of points per unit length.
      phys_size: A tuple with two elements that describe the physical size of
        the entire pattern.
      diameter: A float that represents the diameter of the disc.
      center: A tuple with two elements that describe the coordinates of the
        center of the square.

  Returns:
      An array with Boolean elements.
  """

  phys_size = np.array(phys_size)
  grid_size = phys_size - 1 / resolution
  n = np.round(phys_size * resolution).astype(int)

  x_coord = np.linspace(-grid_size[0] / 2, grid_size[0] / 2, n[0])
  y_coord = np.linspace(-grid_size[1] / 2, grid_size[1] / 2, n[1])
  xv, yv = np.meshgrid(x_coord, y_coord, sparse=True, indexing='ij')

  return (xv - center[0]) ** 2 + (yv - center[1]) ** 2 <= diameter**2 / 4


def stripe(
    resolution: float,
    phys_size: Tuple[float, float],
    width,
    center: Tuple[float, float] = (0, 0),
    angle: float = 0,
) -> np.ndarray:
  """Return a Boolean array where all True elements form a disc.

  Args:
      resolution: A float that represents the number of points per unit length.
      phys_size: A tuple with two elements that describe the physical size of
        the entire pattern.
      width: A float that represents the width of the stripe.
      center: A tuple with two elements that describe the coordinates of the
        center of the stripe.
      angle: A float that represents the angle of rotation in degree.

  Returns:
      An array with Boolean elements.
  """

  phys_size = np.array(phys_size)
  angle = np.radians(angle)

  grid_size = phys_size - 1 / resolution
  n = np.round(phys_size * resolution).astype(int)

  x_coord = np.linspace(-grid_size[0] / 2, grid_size[0] / 2, n[0])
  y_coord = np.linspace(-grid_size[1] / 2, grid_size[1] / 2, n[1])
  xv, yv = np.meshgrid(x_coord, y_coord, sparse=True, indexing='ij')

  return (
      abs(np.sin(angle) * (xv - center[0]) - np.cos(angle) * (yv - center[1]))
      <= width / 2
  )
