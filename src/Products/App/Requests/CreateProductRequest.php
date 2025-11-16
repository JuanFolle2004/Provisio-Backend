<?php

declare(strict_types=1);

namespace Src\Products\App\Requests;
use Illuminate\Foundation\Http\FormRequest;
use Src\Products\Domain\Dtos\ProductDto;

class CreateProductRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'group_id'=>['required', 'integer', 'exists:groups,id'],
            'products'=>['required', 'array'],
            'products.*'=>['required', 'array'],
            'products.*.name'=>['required', 'string'],
            'products.*.amount'=>['required', 'integer', 'min:1'],
            ];
    }

    /**
     * @return array<int, ProductDto>
     */
    public function toDtoArray(): array
    {
        /** @var array<int, array{name: string, amount: int}> $products */
        $products = $this->array('products');
        $dtos = [];
        foreach ($products as $product) {
            $dtos[] = new ProductDto(
                name: $product['name'],
                group_id: $this->integer('group_id'),
                amount: $product['amount'],
            );
        }

        return $dtos;
    }
}
