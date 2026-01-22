#pragma once

#include <vector>
#include <cmath>

class Point {
 private:
  double x_, y_;
  double step_size_ = 0.01;
  Point* target_;
  std::vector<double> pursuit_curve_x_ = {},
                      pursuit_curve_y_ = {};

  const double Distance(const Point* p) const;

 public:
  Point(const double& x, const double& y);
  void Step();
  std::pair<const std::vector<double>&, const std::vector<double>&> GetPursuitCurve() const noexcept;
  const std::pair<double, double> GetCoordinates() const;
  void SetStepSize(const double& step_size);
  void SetTarget(Point* target);
};