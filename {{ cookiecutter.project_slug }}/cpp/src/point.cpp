#include "{{ cookiecutter.module_name }}_core/point.h"

Point::Point(const double& x, const double& y) : x_(x), y_(y) {}

const double Point::Distance(const Point* p) const {
  auto [px, py] = p->GetCoordinates();
  return std::hypot(px - x_, py - y_);  // also from cmath, claimed to be more numerically stable than std::sqrt(x*x + y*y)
}

void Point::Step() {
  auto [tx, ty] = target_->GetCoordinates();
  const double scale = step_size_ / Distance(target_);
  x_ += scale * (tx - x_);
  y_ += scale * (ty - y_);

  pursuit_curve_x_.push_back(x_);
  pursuit_curve_y_.push_back(y_);
}

std::pair<const std::vector<double>&, const std::vector<double>&> Point::GetPursuitCurve() const noexcept {
  return {pursuit_curve_x_, pursuit_curve_y_};
}

const std::pair<double, double> Point::GetCoordinates() const {
  return {x_, y_};
}

void Point::SetStepSize(const double& step_size) {
  step_size_ = step_size;
}

void Point::SetTarget(Point* target) {
  target_ = target;
}
