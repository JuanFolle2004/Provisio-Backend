<?php

declare(strict_types=1);

namespace Src\Assignment\App\Request;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;
use Src\Assignment\Domain\Dtos\AssignDto;

class AssignProductRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'product_id' => ['required', Rule::exists('products', 'id')],
            'group_id' => ['required', Rule::exists('groups', 'id')],
            'amount' => ['required', 'integer', 'min:1'],
            'bought'=>['required', 'integer', 'min:1', 'lte:amount'],
        ];
    }

    public function toDto(): AssignDto
    {
        return new AssignDto(
            productId: $this->integer('product_id'),
            groupId: $this->integer('group_id'),
            amount: $this->integer('amount'),
            bought: $this->integer('bought'),
        );
    }
}
