docker build -t observability-labs/app-tracking-shipping-generator:1.0 src/fake_data_generator
docker run --name app-tracking-shipping-generator-d -p 5006:5006 observability-labs/app-tracking-shipping-generator:1.0