package test

import (
	"fmt"
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

// An example of how to test the simple Terraform module in src using Terratest.
func TestTerraformBasicExample(t *testing.T) {
	t.Parallel()

	username := "rafael.torices"
	backendConfigBucket := fmt.Sprintf("terratest-test-%s", username)
	expectedBucketName := fmt.Sprintf("terratest-lab-%s", username)
	expectedBucketArn := fmt.Sprintf("arn:aws:s3:::%s", expectedBucketName)

	terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
		// The path to where our Terraform code is located
		TerraformDir: "../src",

		// Variables to pass to our Terraform code using -var options
		Vars: map[string]interface{}{
			"username": username,
		},

		// Deploy the module, configuring it to use the S3 bucket as an S3 backend
		BackendConfig: map[string]interface{}{
			"bucket": backendConfigBucket,
			"key":    "eu-central-1/terratest-test-lab.tfstate",
			"region": "eu-central-1",
		},

		// Disable colors in Terraform commands so its easier to parse stdout/stderr
		NoColor: true,
	})

	// Clean up resources with "terraform destroy". Using "defer" runs the command at the end of the test, whether the test succeeds or fails.
	// At the end of the test, run `terraform destroy` to clean up any resources that were created
	defer terraform.Destroy(t, terraformOptions)

	// Run "terraform init" and "terraform apply".
	// This will run `terraform init` and `terraform apply` and fail the test if there are any errors
	terraform.InitAndApply(t, terraformOptions)

	// Run `terraform output` to get the values of output variables
	actualBucketName := terraform.Output(t, terraformOptions, "bucket_name")
	actualBucketArn := terraform.Output(t, terraformOptions, "bucket_arn")

	// Check the output against expected values.
	// Verify we're getting back the outputs we expect
	assert.NotNil(t, expectedBucketName, "it should populate bucket name")
	assert.Equal(t, expectedBucketName, actualBucketName)
	assert.NotNil(t, expectedBucketArn, "it should populate bucket arn")
	assert.Equal(t, expectedBucketArn, actualBucketArn)
}
