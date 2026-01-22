#include <gtest/gtest.h>
#include "{{ cookiecutter.module_name }}_core/point.h"
#include <cmath>

// Test fixture for Point class
class PointTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Setup code if needed
    }

    void TearDown() override {
        // Cleanup code if needed
    }
};

// Test constructor and GetCoordinates
TEST_F(PointTest, ConstructorAndGetCoordinates) {
    Point p(3.0, 4.0);
    auto [x, y] = p.GetCoordinates();
    EXPECT_DOUBLE_EQ(x, 3.0);
    EXPECT_DOUBLE_EQ(y, 4.0);
}

// Test SetStepSize
TEST_F(PointTest, SetStepSize) {
    Point p(0.0, 0.0);
    p.SetStepSize(0.5);
    // Step size is private, but we can test its effect through Step()
    Point target(1.0, 0.0);
    p.SetTarget(&target);
    p.Step();
    auto [x, y] = p.GetCoordinates();
    EXPECT_DOUBLE_EQ(x, 0.5);
    EXPECT_DOUBLE_EQ(y, 0.0);
}

// Test SetTarget and Step
TEST_F(PointTest, SetTargetAndStep) {
    Point p(0.0, 0.0);
    Point target(10.0, 0.0);
    p.SetTarget(&target);
    p.SetStepSize(1.0);
    
    p.Step();
    auto [x, y] = p.GetCoordinates();
    EXPECT_DOUBLE_EQ(x, 1.0);
    EXPECT_DOUBLE_EQ(y, 0.0);
}

// Test Step with diagonal movement
TEST_F(PointTest, StepDiagonal) {
    Point p(0.0, 0.0);
    Point target(3.0, 4.0);  // Distance = 5.0
    p.SetTarget(&target);
    p.SetStepSize(1.0);
    
    p.Step();
    auto [x, y] = p.GetCoordinates();
    EXPECT_NEAR(x, 0.6, 1e-9);  // 3/5 = 0.6
    EXPECT_NEAR(y, 0.8, 1e-9);  // 4/5 = 0.8
}

// Test multiple steps
TEST_F(PointTest, MultipleSteps) {
    Point p(0.0, 0.0);
    Point target(5.0, 0.0);
    p.SetTarget(&target);
    p.SetStepSize(1.0);
    
    for (int i = 0; i < 3; ++i) {
        p.Step();
    }
    
    auto [x, y] = p.GetCoordinates();
    EXPECT_GT(x, 2.0);
    EXPECT_LT(x, 5.0);
    EXPECT_DOUBLE_EQ(y, 0.0);
}

// Test GetPursuitCurve
TEST_F(PointTest, GetPursuitCurve) {
    Point p(0.0, 0.0);
    Point target(10.0, 0.0);
    p.SetTarget(&target);
    p.SetStepSize(1.0);
    
    // Initially empty
    auto [curve_x, curve_y] = p.GetPursuitCurve();
    EXPECT_EQ(curve_x.size(), 0);
    EXPECT_EQ(curve_y.size(), 0);
    
    // After one step
    p.Step();
    auto [curve_x1, curve_y1] = p.GetPursuitCurve();
    EXPECT_EQ(curve_x1.size(), 1);
    EXPECT_EQ(curve_y1.size(), 1);
    EXPECT_DOUBLE_EQ(curve_x1[0], 1.0);
    EXPECT_DOUBLE_EQ(curve_y1[0], 0.0);
    
    // After two steps
    p.Step();
    auto [curve_x2, curve_y2] = p.GetPursuitCurve();
    EXPECT_EQ(curve_x2.size(), 2);
    EXPECT_EQ(curve_y2.size(), 2);
}

// Test pursuit curve tracking
TEST_F(PointTest, PursuitCurveTracking) {
    Point p(0.0, 0.0);
    Point target(3.0, 4.0);
    p.SetTarget(&target);
    p.SetStepSize(0.5);
    
    const int num_steps = 5;
    for (int i = 0; i < num_steps; ++i) {
        p.Step();
    }
    
    auto [curve_x, curve_y] = p.GetPursuitCurve();
    EXPECT_EQ(curve_x.size(), num_steps);
    EXPECT_EQ(curve_y.size(), num_steps);
    
    // Verify curve is monotonically increasing (approaching target)
    for (size_t i = 1; i < curve_x.size(); ++i) {
        EXPECT_GT(curve_x[i], curve_x[i-1]);
        EXPECT_GT(curve_y[i], curve_y[i-1]);
    }
}

// Test negative coordinates
TEST_F(PointTest, NegativeCoordinates) {
    Point p(-5.0, -3.0);
    auto [x, y] = p.GetCoordinates();
    EXPECT_DOUBLE_EQ(x, -5.0);
    EXPECT_DOUBLE_EQ(y, -3.0);
}

// Test zero step size
TEST_F(PointTest, ZeroStepSize) {
    Point p(1.0, 1.0);
    Point target(5.0, 5.0);
    p.SetTarget(&target);
    p.SetStepSize(0.0);
    
    p.Step();
    auto [x, y] = p.GetCoordinates();
    EXPECT_DOUBLE_EQ(x, 1.0);
    EXPECT_DOUBLE_EQ(y, 1.0);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}